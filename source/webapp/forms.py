from django import forms
from webapp.models import Client, Payment, Coach, Group


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'telegram_name',
            'photo',
            'phone',
            'first_name',
            'last_name',
            'email',
            'payment_end_date',
            'region',
            'comment'
        ]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']


class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = [
            'telegram_name',
            'photo',
            'phone',
            'first_name',
            'last_name',
            'email',
            'started_to_work',
            'description'
        ]


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'start_at', 'coach']


class AddClientGroup(forms.Form):
    active_client_id = forms.ModelMultipleChoiceField(
        queryset=Client.objects.active_clients().filter(is_active=True, group__isnull=True),
        label='Клиенты'
    )


class AddGroupClient(forms.Form):
    group_id = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().filter(is_active=True),
        label='Группы:'
    )


class DateInput(forms.DateInput):
    input_type = 'date'


class CoachStatisticsPeriodForm(forms.Form):
    start_date = forms.DateField(required=False, widget=DateInput)
    end_date = forms.DateField(required=False, widget=DateInput)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="Search")


class InviteForm(forms.Form):
    link = forms.URLField(max_length=255)


class GroupMailingForm(forms.Form):
    message = forms.CharField(max_length=1000)


class MailingForm(forms.Form):
    message = forms.CharField(max_length=1000,
                              widget=forms.Textarea(attrs={'rows': '5'}),
                              label='Текст рассылки:')
