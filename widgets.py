from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class PagedownWidget(forms.Textarea):
    class Media:
        css = {
            'all' : ('pagedown/pagedown.css',)
        }
        js = ('%spagedown/Markdown.Converter.js' % settings.STATIC_URL,
              '%spagedown/Markdown.Sanitizer.js' % settings.STATIC_URL,
              '%spagedown/Markdown.Editor.js' % settings.STATIC_URL,
              '%stextarea-resize/textarea-resize.js' % settings.STATIC_URL)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        if 'class' not in attrs:
            attrs['class'] = ""
        attrs['class'] += " wmd-input resizable"
        final_attrs = self.build_attrs(attrs, name=name)
        html = """
            <div class="wmd-wrapper">
                <div class="wmd-panel">
                <div id="%(id)s_wmd_button_bar" class="wmd-button-bar boxsizingBorder"></div>
                <textarea%(attrs)s>%(body)s</textarea>
                </div>
                <h4>Preview:</h4>
                <div id="%(id)s_wmd_preview" class="wmd-panel wmd-preview"></div>
            </div>
            <script type="text/javascript">
                (function () {
                    var converter = Markdown.getSanitizingConverter();
                    selectors = {
                        input : "%(id)s",
                        button : "%(id)s_wmd_button_bar",
                        preview : "%(id)s_wmd_preview",
                    }
                    var editor = new Markdown.Editor(converter, selectors);
                    editor.run();
                    $(document).ready(function() {
                    $('textarea.resizable:not(.processed)').TextAreaResizer();
                    });
                })();
            </script>
            """ % {
                'attrs' : flatatt(final_attrs),
                'body' : conditional_escape(force_unicode(value)),
                'id' : attrs['id'],
            }
        return mark_safe(html)

class AdminPagedownWidget(admin_widgets.AdminTextareaWidget, PagedownWidget):
    class Media:
        css = {
            'all' : ('admin/css/pagedown.css',)
        }
