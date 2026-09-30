from typing import List

from core.models.interests import Page


def build_fb_pages_photo_text_list_for_weapons(pages: List[Page]):
    pages_list = []
    pages_detected = []
    try:
        if not pages:
            return pages_list
        for page in pages:
            source = ""
            cover_source = ""
            try:
                source = (str(page.fb_page_profile_photo)
                          if getattr(page, "fb_page_profile_photo") else source)
            except Exception:
                pass

            try:
                cover_source = (str(page.fb_page_cover_photo)
                                if getattr(page, "fb_page_cover_photo") else cover_source)
            except Exception:
                pass

            if source:
                pages_list.append(
                    {"hash": str(page), "source": source, "text": ""})
                pages_detected.append(page)
            if cover_source:
                pages_list.append(
                    {"hash": str(page), "source": cover_source, "text": ""})
                pages_detected.append(page)
    except Exception:
        pass

    return {'pages_list': pages_list, 'pages_detected': pages_detected}

def build_fb_pages_photo_text_list(pages: List[Page]):
    pages_list = []
    try:
        if not pages:
            return pages_list
        for page in pages:
            source = ""
            cover_source = ""
            try:
                source = (str(page.fb_page_profile_photo)
                          if getattr(page, "fb_page_profile_photo") else source)
            except Exception:
                pass

            text = (page.fb_page_name if getattr(page, "fb_page_name")
                    else "")

            try:
                cover_source = (str(page.fb_page_cover_photo)
                                if getattr(page, "fb_page_cover_photo") else cover_source)
            except Exception:
                pass

            if text or source:
                pages_list.append(
                    {"hash": str(page), "source": source, "text": text})
            if cover_source:
                pages_list.append(
                    {"hash": str(page), "source": cover_source, "text": text})
    except Exception:
        pass

    return pages_list

def build_fb_pages_photo_text_list_extremism(pages: List[Page]):
    pages_list = []
    pages_detected = []
    try:
        if not pages:
            return pages_list
        for page in pages:
            source = ""
            cover_source = ""
            try:
                source = (str(page.fb_page_profile_photo)
                          if getattr(page, "fb_page_profile_photo") else source)
            except Exception:
                pass

            text = (page.fb_page_name if getattr(page, "fb_page_name")
                    else "")

            try:
                cover_source = (str(page.fb_page_cover_photo)
                                if getattr(page, "fb_page_cover_photo") else cover_source)
            except Exception:
                pass

            if text or source:
                pages_list.append(
                    {"hash": str(page), "source": source, "text": text})
                pages_detected.append(page)
            if cover_source:
                pages_list.append(
                    {"hash": str(page), "source": cover_source, "text": text})
                pages_detected.append(page)
    except Exception:
        pass

    return {'pages_list': pages_list, 'pages_detected': pages_detected}

