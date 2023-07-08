from wtforms import Form, StringField, TextAreaField


class PostTextAreaField(TextAreaField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].replace('\r\n', '\n')
        else:
            self.data = ''


class PostForm(Form):
    title = StringField('Title')
    slug = StringField('Slug')
    text = PostTextAreaField('Text', render_kw={'rows':5})