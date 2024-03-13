from rest_framework import serializers

from .models import EvaluatorMetadata, EvaluatorResultSummary


class EventsViewSerializer(serializers.ModelSerializer):
    hits = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EvaluatorMetadata
        fields = ['hits','id','name','description','long_description',
                  'fields_used','fields_display','ipl','crrg_topics',
                  'crrg_page','pdf_page','use_notes','alternative_explanation',
                  'risk_level']

    def get_hits(self, eval):
        return EvaluatorResultSummary.objects.get(evaluator=eval).hits
