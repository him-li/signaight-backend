import re
import string


person_name_redundant_parts = [
    'Ph.D', 'PhD', 'MBA', 'MPhil', 'Cantab', 'GCB.D', 'EMBA', 'Ms. Eng.',
    'Ms', 'Ms.', 'MSc.', 'LL.M.', 'SRMC®', 'AfCGI', 'ASIRS', 'PMP®', 'MA',
    'Dipl.eng.', 'dr.', 'MD', 'M.A.', 'M.A', 'M.S.', 'M.S', 'B.A.', 'B.A',
    'B.S.', 'B.S', 'J.D.', 'J.D', 'Esq.', 'Esq', 'Prof.', 'Prof', 'Sir',
    'Rev.', 'D.D.S.', 'D.D.S', 'D.M.D.', 'D.M.D', 'D.V.M.', 'D.V.M', 'DDS',
    'DMD', 'DO', 'PharmD', 'Pharm.D.', 'Pharm.D', 'PE', 'P.E.', 'CPIM',
    'MCSE', 'P.Eng.', 'CFA', 'CPA', 'CMA', 'CISA', 'CISSP', 'CA', 'CFP',
    'RN', 'R.N.', 'R.N', 'LPN', 'LVN', 'D.O.', 'D.O', 'L.L.C.', 'LLC',
    'Inc.', 'Inc', 'Ltd.', 'Ltd', 'PLC', 'Co.', 'Co', 'B.V.', 'BV', 'GmbH',
    'S.A.', 'SA', 'S.A.S.', 'SAS', 'SpA', 'Spa', 'MSc', 'LL.M', 'dipl. eng.',
    'dipl.', 'eng.', 'eng', 'pmp', 'srmc', 'dr', '®', '😀', '😁', '😂',
    '🤣', '😃', '😄', '😅', '😆', '😉', '😊', '😋', '😎', '😍',
    '😘', '🥰', '😗', '😙', '😚', '🙂', '🤗', '🤩', '🤔', '🤨',
    '😐', '😑', '😶', '🙄', '😏', '😣', '😥', '😮', '🤐', '😯',
    '😪', '😫', '🥱', '😴', '😌', '😛', '😜', '😝', '🤤', '😒',
    '😓', '😔', '😕', '🙃', '🤑', '😲', '☹️', '🙁', '😖', '😞',
    '😟', '😤', '😢', '😭', '😦', '😧', '😨', '😩', '🤯', '😬',
    '😰', '😱', '🥵', '🥶', '😳', '🤪', '😵', '🥴', '😠', '😡',
    '🤬', '🤯', '😷', '🤒', '🤕', '🤢', '🤮', '🤧', '😇', '🥳',
    '🥺', '🥳', '🤠', '😎', '🤓', '🧐', '🌟', '😁', '🧠', '🌸',
    '🚀', '🎓', '🎨', '💼', '🏆', '🧬', '🎻', '🌼', '✈️', '🎈',
    '📚', '🎶', '🐾', '🍀', '⚡', '🌎', '🎉', '🎸', '💡', '⚖️',
    '🌺', '🎤', '🏅', '🚴', '🌷']


def clean_person_name(name, redundant_parts=person_name_redundant_parts):
    try:
        # Normalize input to handle variations
        name = name.lower()

        # Remove redundant parts considering word boundaries and punctuation
        for part in redundant_parts:
            pattern = r'\b' + re.escape(part.lower()) + r'[.,]*\b'
            name = re.sub(pattern, '', name)

        pattern = r'\W®\W?'
        name = re.sub(pattern, '', name)

        # Remove leading/trailing whitespace, punctuation, and extra spaces
        name = re.sub(r'\s+', ' ', name).strip()
        cleaned_name = ''.join(
            char for char in name if char not in string.punctuation).strip()

        # Capitalize the cleaned name
        cleaned_name = ' '.join(word.capitalize()
                                for word in cleaned_name.split())

        return cleaned_name
    except Exception:
        return name
