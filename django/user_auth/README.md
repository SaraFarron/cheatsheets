### Dependencies

    Django

### HTML files

login.html

    {% extends 'base.html' %}

    {% block content %}
    <h2>Login</h2>
    <form method="post">
        {% csrf_token %}
        {% for field in form %}
        <p>
            {{ field.label_tag }}<br>
            {{ field }}
            {% if field.help_text %}
            <small style="color: grey">{{ field.help_text }}</small>
            {% endif %}
            {% for error in field.errors %}
            <p style="color: red">{{ error }}</p>
            {% endfor %}
        </p>
        {% endfor %}
        <button type="submit">Login</button>
    </form>
    {% endblock %}

register.html

    {% extends 'base.html' %}

    {% block content %}
    <h2>Sign up</h2>
    <form method="post">
        {% csrf_token %}
        {% for field in form %}
        <p>
            {{ field.label_tag }}<br>
            {{ field }}
            {% if field.help_text %}
            <small style="color: grey">{{ field.help_text }}</small>
            {% endif %}
            {% for error in field.errors %}
            <p style="color: red">{{ error }}</p>
            {% endfor %}
        </p>
        {% endfor %}
        <button type="submit">Sign up</button>
    </form>
    {% endblock %}

profile.html

    {% extends 'base.html' %}

    {% block content %}
    <h2>Profile</h2>
    Hello, {{ user }}
    {% endblock %}

base.html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>user_auth</title>
    </head>
    <body>

    <!-- Page Content -->
    <div>
    {% block content %}

    {% endblock %}
    </div>
    <!-- /.container -->

    </body>
</html>