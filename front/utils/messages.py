from django.utils.html import format_html
import markdown


def convert_md_to_html(message):
    return format_html(markdown.markdown(message))
