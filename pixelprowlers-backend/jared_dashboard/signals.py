from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Manifesto, ManifestoVersion

@receiver(pre_save, sender=Manifesto)
def enforce_single_active_manifesto(sender, instance, **kwargs):
    """
    Garantit qu’un seul manifeste est actif à la fois.
    Si un nouveau manifeste est défini comme 'current', alors les autres sont désactivés
    et le précédent est archivé.
    """
    if instance.current:
        # Cherche les autres manifestes actifs
        previous_active = Manifesto.objects.filter(current=True).exclude(pk=instance.pk)

        for old_manifest in previous_active:
            # Crée une archive dans ManifestoVersion
            ManifestoVersion.objects.create(
                manifesto=old_manifest,
                version=old_manifest.version,
                content=old_manifest.content,
                archived_by="System (auto-archive)"
            )
            # Désactive l'ancien manifeste
            old_manifest.current = False
            old_manifest.save(update_fields=["current"])
