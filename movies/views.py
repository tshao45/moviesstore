from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition
from django import forms
from django.contrib.auth.decorators import login_required
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    movies = movies.exclude(amount_left = 0)

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})
def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

# Additional views for Petition can be added here

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['movie_name', 'description']  
@login_required
def view_petitions(request):
    template_data = {}
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.user = request.user
            petition.save()
        else:
            form = PetitionForm()
    petitions = Petition.objects.all().order_by('-date')
    template_data["petitions"] = petitions
    template_data["form"] = PetitionForm()
    return render(request, 'movies/petition.html', {'petitions': petitions})
@login_required
def approve_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    if request.user in petition.voters.all():
        return redirect('movies.view_petitions')
    petition.votes += 1
    petition.voters.add(request.user)
    petition.save()
    return redirect('movies.view_petitions')