import inspect
from dataclasses import dataclass


@dataclass
class Round:
    id: str
    fund_id: str
    title: str
    short_name: str
    prospectus: str
    privacy_notice: str
    support_times: str
    support_days: str
    instructions: str
    project_name_field_id: str
    opens: str | None = None
    deadline: str | None = None
    assessment_deadline: str | None = None
    contact_phone: str | None = None
    contact_email: str | None = None
    contact_textphone: str | None = None
    feedback_link: str | None = None
    application_guidance: str | None = None
    guidance_url: str | None = None
    all_uploaded_documents_section_available: bool = False
    application_fields_download_available: bool = False
    display_logo_on_pdf_exports: bool = False
    requires_feedback: bool = False
    mark_as_complete_enabled: bool = False

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            **{
                k: v
                for k, v in d.items()
                if k in inspect.signature(cls).parameters and v is not None
            }
        )
