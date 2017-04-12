from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Review, Mineral_Water, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters

import datetime

from django.contrib.auth.decorators import login_required


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def mineralwater_list(request):
    mineralwater_list = Mineral_Water.objects.order_by('-name')
    context = {'mineralwater_list': mineralwater_list}
    return render(request, 'reviews/mineralwater_list.html', context)


def mineralwater_detail(request, mineralwater_id):
    mineralwater = get_object_or_404(Mineral_Water, pk=mineralwater_id)
    form = ReviewForm()
    return render(request, 'reviews/mineralwater_detail.html', {'mineralwater': mineralwater, 'form': form})


@login_required
def add_review(request, mineralwater_id):
    mineralwater = get_object_or_404(Mineral_Water, pk=mineralwater_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.mineralwater = mineralwater
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        return HttpResponseRedirect(reverse('reviews:mineralwater_detail', args=(mineralwater.id,)))

    return render(request, 'reviews/mineralwater_detail.html', {'mineralwater': mineralwater, 'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list': latest_review_list, 'username': username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('mineralwater')
    user_reviews_mineralwater_ids = set(map(lambda x: x.mineralwater.id, user_reviews))


    try:
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name
    except:
        update_clusters()
        user_cluster_name = User.objects.get(username=request.user.username).cluster_set.first().name

    user_cluster_other_members = Cluster.objects.get(name=user_cluster_name).users.exclude(
        username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    other_users_reviews = Review.objects.filter(user_name__in=other_members_usernames).exclude(
        mineralwater__id__in=user_reviews_mineralwater_ids)
    other_users_reviews_mineralwater_ids = set(map(lambda x: x.mineralwater.id, other_users_reviews))

    mineralwater_list = sorted(
        list(Mineral_Water.objects.filter(id__in=other_users_reviews_mineralwater_ids)),
        key=lambda x: x.average_rating,
        reverse=True
    )

    return render(
        request,
        'reviews/userrecommendation_list.html',
        {'username': request.user.username, 'mineralwater_list': mineralwater_list}
    )

