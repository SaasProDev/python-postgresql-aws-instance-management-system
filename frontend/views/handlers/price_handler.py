from django.conf import settings

HOURS_IN_MONTH = settings.HOURS_IN_MONTH


def counts_calculate(info, label, results, apply_billing=True):
    for item in results:
        try:
            status = item['status']
            if not info[label].get(status):
                info[label][status] = 0
            info[label][status] += 1
            info[label]['total'] += 1
            if item.get('applications'):
                info[label]['total'] = len(item['applications'])
            if apply_billing and item.get('billing'):
                info[label]['billing']['total'] += item['billing']['total']
                info[label]['billing']['rate_month'] += item['billing']['rate_month']
        except:
            print("SOMETHING HAPPENED IN calculate")
            pass

    info[label]['billing']['total'] = round(info[label]['billing']['total'], 4)
    info[label]['billing']['rate_month'] = round(info[label]['billing']['rate_month'], 2)


def empty_billing_info():
    return dict(counts={
        'iaas': {
            'total': 0,
            'failed': 0,
            'successful': 0,
            'running': 0,
            'billing': {
                'total': 0,
                'rate_month': 0
            }
        },
        'virtualmachines': {
            'total': 0,
            'failed': 0,
            'successful': 0,
            'running': 0,
            'billing': {
                'total': 0,
                'rate_month': 0
            }
        },
        'applications': {
            'total': 0,
            'failed': 0,
            'successful': 0,
            'running': 0,
            'billing': {
                'total': 0,
                'rate_month': 0
            }
        },
    })
