from .base_job_models import JobEvent
from .models_general import Tag, Container, WizardBox
from .models_jobtask import RunnerTask, Job
from .models_device import Device
from .models_device_based import NetworkGear, VirtualMachine
from .models_billing import ResourceAliveHistory

from .models_job_based import(
    IaaS,
    PaaS,
    Sdn,
    Provider,
    Storage,
    Billing,
    Backup,
    Pki,
    Security,
    Monitoring,
    Service,
    UserCredential,
    Documentation
)

from .models_network import (IPAddress, Aggregate, Vlan, Prefix, Vrf, Rir)
from .models_credential import (Credential, UserSecret, UserKey)
# from .models_project import (Project, UserProject, Infrastructure)
from .models_project import (Project, UserProject)


IMPORTANT_MODELS = (
    IaaS,
    PaaS,
    Sdn,
    IPAddress,
    Prefix,
    Device,
    NetworkGear,
    Rir,
    Vlan,
    Vrf,
    VirtualMachine,
    Job,
    JobEvent,
    Provider,
    Storage,
    Tag,
    Aggregate,
    Container,
    WizardBox,
    Credential,
    Documentation,
    RunnerTask,
    Billing,
    Backup,
    Pki,
    Security,
    Monitoring,
    Service,
    UserSecret,
    UserKey,
    UserCredential,

    ResourceAliveHistory
)
