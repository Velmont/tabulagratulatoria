from django.contrib.admin.widgets import AdminIntegerFieldWidget


class NumberWidget(AdminIntegerFieldWidget):
    class_name = 'NumberWidget'
    input_type = 'number'

    def __init__(self, attrs=None):
        final_attrs = {'min': 0, 'step': 1}
        if attrs is not None:
            final_attrs.update(attrs)
        super(NumberWidget, self).__init__(attrs=final_attrs)
