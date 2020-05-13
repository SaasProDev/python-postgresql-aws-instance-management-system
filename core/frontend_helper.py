import logging

_logger = logging.getLogger(__name__)


def organization_from_form(user, *args, **kwargs):
    from account.models import Organization

    form_data = kwargs.get('form_data')
    uuid = form_data.get('project_organisation')
    organization = Organization.objects.filter(uuid=uuid).first()

    if not organization:
        mess = "Invalid Organization uuid '{}' passed to a Form.".format(uuid)
        _logger.error(mess)
        raise Exception(mess)

    if user.check_is_available_object(organization, mode='grant'):
        return organization
    else:
        mess = "User have no asses to Organization uuid: '{}'!".format(uuid)
        _logger.error(mess)
        raise Exception(mess)
