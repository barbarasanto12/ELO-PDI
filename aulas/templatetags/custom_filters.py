from django import template

register = template.Library()

@register.filter
def get_feedback_value(feedback, campo):
    """
    Retorna o valor de um campo específico de feedback.
    """
    return getattr(feedback, campo, None)
