# coding=utf-8
"""按章节拆分长文本、分段语音合成、再用本机 ffmpeg 合并为完整音频。

单次合成调用长度上限为 10000 字符，脚本会先按 Markdown 标题切分章节，
再把章节装箱成不超过上限的片段依次合成，最后用 ffmpeg concat 合并。

运行前需配置环境变量 DASHSCOPE_API_KEY（鉴权）与 DASHSCOPE_WORKSPACE_ID（业务空间 ID）。

用法::

    python test.py -i ./chapters/test.md
    python test.py -i ./chapters/test.md -o ./chapters/test.md.mp3
    python test.py -i ./chapters/test.md --force --keep-parts
    python test.py -i ./chapters/test.md --bgm ./bgm.mp3 --bgm-volume 0.2
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

# If the API Key is not configured in the environment variable, your-api-key needs to be replaced with your own API Key
# dashscope.api_key = "your-api-key"

# websocket 地址在 main() 中根据环境变量 DASHSCOPE_WORKSPACE_ID 拼接，未配置时提示退出
WORKSPACE_ID_ENV = 'DASHSCOPE_WORKSPACE_ID'
BASE_WS_URL_TEMPLATE = 'wss://{}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'

DEFAULT_MODEL = "qwen-audio-3.0-tts-flash"
# Please enter the correct voice below.
DEFAULT_VOICE = "longanhuan_v3.6"
# 背景音乐默认音量（0.2，避免盖过人声）
DEFAULT_BGM_VOLUME = 0.2

# 单次调用的最大字符数
MAX_CHARS = 10000
# 合成失败重试次数与间隔（秒）
MAX_RETRIES = 3
RETRY_INTERVAL = 3

HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$')
SENTENCE_RE = re.compile(r'[^。！？；.!?;\n]+[。！？；.!?;\n]?')


def split_chapters(text):
    """按 Markdown 标题切分为 [(标题, 正文)]，首个标题前的内容归入“前言”。"""
    chapters = []
    title, buf = '前言', []
    for line in text.splitlines(keepends=True):
        matched = HEADING_RE.match(line)
        if matched:
            if buf:
                chapters.append((title, ''.join(buf)))
            title, buf = matched.group(2), [line]
        else:
            buf.append(line)
    if buf:
        chapters.append((title, ''.join(buf)))
    return chapters


def split_sentences(block, max_chars):
    """把超长段落按句拆成不超过 max_chars 的片段，极端情况按字符硬切。"""
    pieces, cur = [], ''
    for sentence in SENTENCE_RE.findall(block):
        while len(sentence) > max_chars:
            if cur:
                pieces.append(cur)
                cur = ''
            pieces.append(sentence[:max_chars])
            sentence = sentence[max_chars:]
        if len(cur) + len(sentence) <= max_chars:
            cur += sentence
        else:
            if cur:
                pieces.append(cur)
            cur = sentence
    if cur:
        pieces.append(cur)
    return pieces


def split_paragraphs(content, max_chars):
    """把超长章节按空行分段，必要时再按句拆分，保证每片不超过 max_chars。"""
    paragraphs = [p for p in re.split(r'\n\s*\n', content) if p.strip()]
    pieces, cur = [], ''
    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if cur:
                pieces.append(cur)
                cur = ''
            pieces.extend(split_sentences(paragraph, max_chars))
            continue
        merged = (cur + '\n\n' + paragraph) if cur else paragraph
        if len(merged) <= max_chars:
            cur = merged
        else:
            pieces.append(cur)
            cur = paragraph
    if cur:
        pieces.append(cur)
    return pieces


def make_chunks(chapters, max_chars):
    """按章节顺序装箱，返回 [{'titles': [...], 'text': ...}]，每片长度不超过 max_chars。"""
    chunks, cur_parts, cur_len = [], [], 0

    def flush():
        nonlocal cur_parts, cur_len
        if cur_parts:
            chunks.append({
                'titles': [title for title, _ in cur_parts],
                'text': '\n\n'.join(text for _, text in cur_parts),
            })
            cur_parts, cur_len = [], 0

    for title, body in chapters:
        pieces = [body] if len(body) <= max_chars else split_paragraphs(body, max_chars)
        for index, piece in enumerate(pieces, start=1):
            label = title if len(pieces) == 1 else '{}（{}/{}）'.format(title, index, len(pieces))
            extra = 2 if cur_parts else 0
            if cur_len + extra + len(piece) > max_chars:
                flush()
                extra = 0
            cur_parts.append((label, piece))
            cur_len += extra + len(piece)
    flush()
    return chunks


def synthesize(text, model, voice):
    """调用一次语音合成，失败时重试，返回音频字节。"""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            synthesizer = SpeechSynthesizer(model=model, voice=voice)
            try:
                audio = synthesizer.call(text)
            finally:
                close = getattr(synthesizer, 'close', None)
                if callable(close):
                    close()
            if not audio:
                raise RuntimeError('返回的音频内容为空')
            return audio
        except Exception as exc:  # 网络抖动、服务限流等均重试
            last_error = exc
            print('  第 {}/{} 次合成失败: {}'.format(attempt, MAX_RETRIES, exc), file=sys.stderr)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_INTERVAL)
    raise RuntimeError('语音合成失败: {}'.format(last_error))


def merge_audio(part_files, output, ffmpeg):
    """借助 ffmpeg concat 合并分段音频，优先流拷贝，失败后转为重新编码。"""
    list_file = output + '.concat.txt'
    with open(list_file, 'w', encoding='utf-8') as f:
        for path in part_files:
            f.write("file '{}'\n".format(os.path.abspath(path).replace('\\', '/').replace("'", "'\\''")))

    base_cmd = [ffmpeg, '-y', '-hide_banner', '-loglevel', 'error',
                '-f', 'concat', '-safe', '0', '-i', list_file]
    last_error = ''
    for encode_args in (['-c', 'copy'], ['-c:a', 'libmp3lame', '-q:a', '2']):
        result = subprocess.run(base_cmd + encode_args + [output], capture_output=True, text=True)
        if result.returncode == 0:
            print('合并方式: ffmpeg {}'.format(' '.join(encode_args)))
            os.remove(list_file)
            return
        last_error = result.stderr.strip() or '返回码 {}'.format(result.returncode)
        print('ffmpeg {} 失败，尝试其他方式: {}'.format(' '.join(encode_args), last_error), file=sys.stderr)

    raise RuntimeError('ffmpeg 合并失败: {}'.format(last_error))


def mix_audio(master_path, bgm_path, output, ffmpeg, bgm_volume):
    """把循环铺满的背景音乐与主音轨混音，背景音量默认 0.2，避免盖过人声。"""
    filter_complex = ('[0:a]volume=1.0[tts];'
                      '[1:a]volume={}[bgm];'
                      '[tts][bgm]amix=inputs=2:duration=shortest:dropout_transition=0[out]').format(bgm_volume)
    cmd = [ffmpeg, '-y', '-hide_banner', '-loglevel', 'error',
           '-i', master_path, '-stream_loop', '-1', '-i', bgm_path,
           '-vn', '-filter_complex', filter_complex,
           '-map', '[out]', '-c:a', 'libmp3lame', '-b:a', '128k',
           '-ar', '44100', '-ac', '2', output]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError('ffmpeg 混音失败: {}'.format(result.stderr.strip() or result.returncode))


def resolve_websocket_url():
    """从环境变量 DASHSCOPE_WORKSPACE_ID 拼接 websocket 地址，未配置时提示退出。"""
    workspace_id = os.getenv(WORKSPACE_ID_ENV, '').strip()
    if not workspace_id:
        raise SystemExit(
            '未配置环境变量 {}，请先设置为百炼业务空间 ID 后重试，例如：\n'
            '  Windows 临时生效: set {}=你的业务空间ID\n'
            '  Windows 永久生效: setx {}=你的业务空间ID\n'
            '  Linux/macOS: export {}=你的业务空间ID'.format(
                WORKSPACE_ID_ENV, WORKSPACE_ID_ENV, WORKSPACE_ID_ENV, WORKSPACE_ID_ENV))
    return BASE_WS_URL_TEMPLATE.format(workspace_id)


def build_output_path(input_path):
    return os.path.splitext(input_path)[0] + '.mp3'


def main(argv=None):
    parser = argparse.ArgumentParser(description="""
    Markdown 文档的 TTS 语音合成
    基于阿里百炼平台 TTS 语言合成
    对 Markdown 章节分段语音合成并用 ffmpeg 合并
    支持背景音乐混音
    使用前
    请先在百炼平台获取自己的业务空间ID，并设置为环境变量 DASHSCOPE_WORKSPACE_ID=llm-xxx
    再获取自己的模型调用的 ApiKey，并设置为环境变量 DASHSCOPE_API_KEY=sk-xxx
    """)
    parser.add_argument('-i', '--input', required=True, help='输入 Markdown 文件（必填）')
    parser.add_argument('-o', '--output', default=None, help='输出 mp3 路径，默认与输入文件同名')
    parser.add_argument('--max-chars', type=int, default=MAX_CHARS, help='单次调用最大字符数，默认 10000')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='语音合成模型')
    parser.add_argument('--voice', default=DEFAULT_VOICE, help='音色')
    parser.add_argument('--bgm', default=None, help='背景音乐文件路径，不指定则不混音')
    parser.add_argument('--bgm-volume', type=float, default=DEFAULT_BGM_VOLUME,
                        help='背景音乐音量，取值 (0, 1]，默认 {}'.format(DEFAULT_BGM_VOLUME))
    parser.add_argument('--ffmpeg', default='ffmpeg', help='ffmpeg 可执行文件路径，默认取环境变量 PATH')
    parser.add_argument('--work-dir', default=None, help='分段音频目录，默认 <输出文件名>.parts')
    parser.add_argument('--keep-parts', action='store_true', help='合并完成后保留分段音频')
    parser.add_argument('--force', action='store_true', help='忽略已存在的分段音频，强制重新合成')
    args = parser.parse_args(argv)

    input_path = os.path.abspath(args.input)
    if not os.path.isfile(input_path):
        parser.error('输入文件不存在: {}'.format(input_path))
    output_path = os.path.abspath(args.output or build_output_path(input_path))
    work_dir = os.path.abspath(args.work_dir or output_path + '.parts')

    bgm_path = os.path.abspath(args.bgm) if args.bgm else None
    if bgm_path and not os.path.isfile(bgm_path):
        parser.error('背景音乐文件不存在: {}'.format(bgm_path))
    if bgm_path and not 0 < args.bgm_volume <= 1:
        parser.error('--bgm-volume 需大于 0 且不超过 1（默认 0.2），避免背景音乐盖过人声')

    if shutil.which(args.ffmpeg) is None and not os.path.isfile(args.ffmpeg):
        parser.error('未找到 ffmpeg，请用 --ffmpeg 指定可执行文件路径')

    api_key = os.getenv('DASHSCOPE_API_KEY')
    if api_key:
        dashscope.api_key = api_key
    dashscope.base_websocket_api_url = resolve_websocket_url()

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    chapters = split_chapters(content)
    chunks = make_chunks(chapters, args.max_chars)
    print('文件 {} 共 {} 字符、{} 个章节，拆分为 {} 个片段'.format(
        os.path.basename(input_path), len(content), len(chapters), len(chunks)))

    os.makedirs(work_dir, exist_ok=True)
    manifest_path = os.path.join(work_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump([{'index': index, 'titles': chunk['titles'], 'chars': len(chunk['text']),
                    'file': 'part_{:03d}.mp3'.format(index)}
                   for index, chunk in enumerate(chunks, start=1)], f, ensure_ascii=False, indent=2)

    part_files = []
    for index, chunk in enumerate(chunks, start=1):
        part_path = os.path.join(work_dir, 'part_{:03d}.mp3'.format(index))
        if os.path.exists(part_path) and os.path.getsize(part_path) > 0 and not args.force:
            print('[{}/{}] 已存在，跳过: {}'.format(index, len(chunks), chunk['titles'][0]))
            part_files.append(part_path)
            continue
        print('[{}/{}] {} 字符 | {}'.format(index, len(chunks), len(chunk['text']), chunk['titles'][0]))
        audio = synthesize(chunk['text'], args.model, args.voice)
        with open(part_path, 'wb') as f:
            f.write(audio)
        part_files.append(part_path)

    if bgm_path:
        master_path = os.path.join(work_dir, 'master.mp3')
        merge_audio(part_files, master_path, args.ffmpeg)
        mix_audio(master_path, bgm_path, output_path, args.ffmpeg, args.bgm_volume)
        print('混音完成（背景音量 {}）: {}'.format(args.bgm_volume, output_path))
    else:
        merge_audio(part_files, output_path, args.ffmpeg)
        print('合并完成: {}'.format(output_path))

    if not args.keep_parts:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
