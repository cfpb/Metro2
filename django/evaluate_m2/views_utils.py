from django.conf import settings
from django.contrib.auth.models import User

from django_application.s3_utils import s3_resource

def has_permissions_for_request(request, event) -> bool:
    if settings.SSO_ENABLED:
        user = User.objects.get(username=request.user.username)
        return event.check_access_for_user(user)
    else:
        return True

def get_randomizer(result_total, total_per_page) -> int:
    randomizer = 1
    if result_total > total_per_page:
        randomizer = result_total // total_per_page
    return randomizer

def random_sample_id_list(eval_result_summary, number_of_results):
    randomizer = get_randomizer(eval_result_summary.hits, number_of_results)

    final_index = randomizer * number_of_results

    eval_result_sample = eval_result_summary.evaluatorresult_set \
        .only('source_record_id') \
        .order_by('id')[0:final_index:randomizer]

    return [result.source_record_id for result in eval_result_sample]
