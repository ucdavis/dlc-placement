from django.http import HttpResponse

def health(request):
	print("HEALTH")
	return HttpResponse(status=200)