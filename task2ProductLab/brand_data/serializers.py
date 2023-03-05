from rest_framework import serializers


class FileOrNumberSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    number = serializers.IntegerField(required=False)

    def validate(self, data):
        if not data.get('file') and not data.get('number'):
            raise serializers.ValidationError("Either 'file' or 'number' field must be provided.")
        if data.get('file') and data.get('number'):
            raise serializers.ValidationError("Only one of 'file' or 'number' fields can be provided.")
        if data.get('file') and not data.get('file').name.endswith('.xlsx'):
            raise serializers.ValidationError("The file must be in .xlsx format.")

        return data
