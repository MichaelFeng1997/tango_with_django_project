from django.shortcuts import render
from rango.models import Category
# Create your views here.
#from django.http import HttpResponse
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
def show_category(request,category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception
        # So the .get() method returns one model instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category = category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary
        # we'll use this in the template to verify that the category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything

        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.
    return render(request,'rango/category.html',context_dict)

def index(request):
    # Query the database for a list of ALL categories currently
    # Order the categories by no. likes in descending order
    # Retrieve the top 5 only - or all if less than 5
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list,'pages':page_list}
    return render(request, 'rango/index.html',context = context_dict)

def about(request):
    # print out whether the method is a GET or a POST
    print(request.method)
    #print out the user name, if no one is logged in it prints 'AnonymousUser'
    print(request.user)
    return render(request, 'rango/about.html',{})


def add_category(request):
    form = CategoryForm()

    # AHTTP Post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provideed with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            cat = form.save(commit=True)
            print(cat,cat.slug)
            # Now that the category is saved
            # We could give a confirmation message #
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # the supplied form contained errors
            # just print them to the terminal
            print(form.errors)

    return render(request,'rango/add_category.html',{'form':form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)