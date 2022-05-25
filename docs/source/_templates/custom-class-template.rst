{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:
   :inherited-members:

   {% block methods %}
   {% if methods %}
   .. rubric:: {{ _('Public Methods') }}

   .. autosummary::
      :nosignatures:
      {% for item in (all_methods) %}
        {%- if not item.startswith('_') and not item.endswith('__') %}
            ~{{ name }}.{{ item }}
        {% endif %}
      {%- endfor %}

   .. rubric:: {{ _('Private Methods') }}

   .. autosummary::
      :nosignatures:
      {% for item in (all_methods) %}
        {%- if item.startswith('_') and not item.endswith('__') %}
            ~{{ name }}.{{ item }}
        {% endif %}
      {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
