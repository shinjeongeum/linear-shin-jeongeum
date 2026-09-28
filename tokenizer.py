"""
Linear Shin-Jeongeum Tokenizer (선형 신정음 토크나이저)
Hardware-Native 1D Phonetic Tokenization for Multilingual Speech-to-Text AI Models.
Patent Priority Secured (KIPO, 2026).
"""

from typing import List

# 초성(19자), 중성(21자), 종성(28자, 종성 없음 포함) 유니코드 오프셋 상수
CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 
    'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

JUNGSUNG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 
    'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
]

JONGSUNG_LIST = [
    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 
    'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

# 한어병음 성조 기호 맵핑 (-: 1성, /: 2성, v: 3성, \: 4성)
PINYIN_TONE_MAP = {
    'ā': ('a', '-'), 'á': ('a', '/'), 'ǎ': ('a', 'v'), 'à': ('a', '\\'),
    'ē': ('e', '-'), 'é': ('e', '/'), 'ě': ('e', 'v'), 'è': ('e', '\\'),
    'ī': ('i', '-'), 'í': ('i', '/'), 'ǐ': ('i', 'v'), 'ì': ('i', '\\'),
    'ō': ('o', '-'), 'ó': ('o', '/'), 'ǒ': ('o', 'v'), 'ò': ('o', '\\'),
    'ū': ('u', '-'), 'ú': ('u', '/'), 'ǔ': ('u', 'v'), 'ù': ('u', '\\'),
    'ǖ': ('v', '-'), 'ǘ': ('v', '/'), 'ǚ': ('v', 'v'), 'ǜ': ('v', '\\'),
}

class LinearShinJeongeumTokenizer:
    def __init__(self):
        self.chosung = CHOSUNG_LIST
        self.jungsung = JUNGSUNG_LIST
        self.jongsung = JONGSUNG_LIST

    def decompose_hangul(self, char: str) -> List[str]:
        """2차원 조합형 한글 음절을 1차원 선형 음소 시퀀스로 완전 분해"""
        code = ord(char)
        if 0xAC00 <= code <= 0xD7A3:
            s_index = code - 0xAC00
            cho = s_index // 588
            jung = (s_index % 588) // 28
            jong = s_index % 28
            
            res = [self.chosung[cho], self.jungsung[jung]]
            if jong > 0:
                res.append(self.jongsung[jong])
            return res
        return [char]

    def encode(self, text: str) -> List[str]:
        """한국어 문장을 1차원 선형 신정음 토큰 시퀀스로 인코딩"""
        tokens = []
        for char in text:
            tokens.extend(self.decompose_hangul(char))
        return tokens

    def encode_pinyin(self, pinyin: str) -> List[str]:
        """중국어 병음을 권설음 및 1차원 성조 기하 좌표계로 인코딩"""
        tokens = []
        tone = None
        cleaned_chars = []
        
        for c in pinyin:
            if c in PINYIN_TONE_MAP:
                base_char, tone_marker = PINYIN_TONE_MAP[c]
                cleaned_chars.append(base_char)
                tone = tone_marker
            else:
                cleaned_chars.append(c)
                
        p_str = "".join(cleaned_chars)
        
        # 권설음 및 1차원 신정음 음소 정렬
        if p_str.startswith("zh"):
            tokens.append("ㅈ=")
            p_str = p_str[2:]
        elif p_str.startswith("ch"):
            tokens.append("ㅊ=")
            p_str = p_str[2:]
        elif p_str.startswith("sh"):
            tokens.append("ㅅ=")
            p_str = p_str[2:]
            
        for ch in p_str:
            if ch == 'o':
                tokens.append('ㅗ')
            elif ch == 'u':
                tokens.append('ㅜ')
            elif ch == 'n' and p_str.endswith('ng'):
                pass
            elif ch == 'g' and p_str.endswith('ng'):
                tokens.append('ㅇ')
            else:
                tokens.append(ch)
                
        if tone:
            tokens.append(tone)
            
        return tokens
