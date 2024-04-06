.. Describes the workflow how to setup navbars.

Navbar
======

This follows the documentation here: https://getbootstrap.com/docs/5.2/components/navbar/

.. code-block: html
{% block navbar %}
    <nav class="navbar navbar-expand-xxl navbar-dark bg-dark">
        <div class="container-fluid">
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <p>{{ nav_bar_escape }}</p>
            <ul class="navbar-nav me-auto">
                <li class="{{ nav.type }}">
                    <a class="nav-link dropdown-toggle" href="{{ nav_bar_escape }}/{{ nav.url }}" role="button" data-bs-toggle="dropdown" aria-expanded="false">{{ nav.name }}</a>
                    <ul class="dropdown-menu">
                        <li>
                            <a class="dropdown-item" href="{{ drop.url }}">{{ drop.name }}</a>
                        </li>
                    </ul>
                </li>
            </ul>
            {% if user.is_authenticated %}
            <span class="navbar-text">
                {{user.username}}
            </span>
            <form id="logoutform" method="POST" action="accounts/logout/">
                {% csrf_token %}
                <button type="submit" class="btn btn-info">Logout</button>
            </form>
            {% endif %}
        </div>
        </div>
    </nav>
{% endblock %}