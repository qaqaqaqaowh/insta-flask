from flask import render_template


def render(template, **kwargs):
    def render_content():
        return render_template(template, **kwargs)
    return render_template("layout.html", render=render_content, **kwargs)
