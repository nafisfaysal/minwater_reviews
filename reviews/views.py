from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ReviewForm
import datetime
from .models import Review,Mineral_Water

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'lastest_review_list':latest_review_list}
    return render(request,'reviews/review_list.html',context)


def review_detail(request,review_id):
    review = get_object_or_404(Review,pk = review_id)
    return render(request,'reviews/review_detail.html',{'review': review})


def mineralwater_list(request):
    mineralwater_list = Mineral_Water.objects.order_by('-name')
    context = {'mineralwater_list':mineralwater_list}
    return render(request, 'reviews/mineralwater_list.html',context)


def mineralwater_detail(request,mineralwater_id):
    mineralwater = get_object_or_404(Mineral_Water, pk=mineralwater_id)
    form = ReviewForm()
    return render(request, 'reviews/mineralwater_detail.html', {'mineralwater': mineralwater, 'form': form})


def add_review(request,mineralwater_id):
    mineralwater = get_object_or_404(Mineral_Water, pk = mineralwater_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['raing']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        review = Review()
        review.mineralwater = mineralwater
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect(reverse('reviews:mineralwater_detail',args=(mineralwater.id,)))

    return render(request,'reviews/mineralwater_detail.html', {'mineralwater':mineralwater, 'form':form})
