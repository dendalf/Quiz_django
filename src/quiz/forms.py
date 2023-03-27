from django import forms
from django.core.exceptions import ValidationError

from .models import Choice


class QuestionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):

        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):

            raise ValidationError(
                f'Questions count must be range '
                f'from {self.instance.QUESTION_MIN_LIMIT} '
                f'to {self.instance.QUESTION_MAX_LIMIT} inclusive'
            )

        order_num_list = []
        range_list = []
        for index, form in enumerate(self.forms):
            order_num_list.append(form.cleaned_data['order_num'])
            range_list.append(index + 1)
        sorted_order_num_list = sorted(order_num_list)
        if not (sorted_order_num_list == range_list and sorted_order_num_list[-1] <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                f'Order number must not be from 1 to 100 and less than '
                f'{self.instance.QUESTION_MAX_LIMIT} inclusive'
            )


class ChoiceInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        num_correct_answers = sum(form.cleaned_data['is_correct'] for form in self.forms)

        if num_correct_answers == 0:
            raise ValidationError('You must select at least 1 option.')

        if num_correct_answers == len(self.forms):
            raise ValidationError('NOT allowed to select all options.')


class ChoiceForm(forms.ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text']


ChoicesFormSet = forms.modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
