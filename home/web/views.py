from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Title, Datatable, Category, Report_price, Cart


class HomeView(View):
    def get(self, request):
        titles = Title.objects.all()  # Fetch all reports
        return render(request, 'index.html', {'titles': titles})


class ReportDetailView(View):
    def get(self, request, rep_id, url_slug):
        title = get_object_or_404(Title, rep_id=rep_id)
        datatable = get_object_or_404(Datatable, rep_id=rep_id)
        category = get_object_or_404(Category, rep_category_id=title.rep_category_id)
        buying_options = Report_price.objects.all()

        context = {
            'title': title,
            'datatable': datatable,
            'category_name': category.category_name,
            'buying_options': buying_options
        }

        return render(request, 'info.html', context)


class AddToCartView(View):
    def post(self, request, rep_id):
        title = get_object_or_404(Title, rep_id=rep_id)
        selected_option = request.POST.get('license')

        if not selected_option:
            return render(request, 'error.html', {'message': 'No license option selected.'})

        price = get_object_or_404(Report_price, label=selected_option)

        # Check if report is already in the cart
        cart_item, created = Cart.objects.get_or_create(
            rep_id=title,
            defaults={
                'rep_title': title.rep_title,
                'price': price.price,
                'label': price.label,
            }
        )

        if not created:
            # Update the price if the item already exists in the cart
            cart_item.price = price.price
            cart_item.label = price.label
            cart_item.save()

        return redirect('cart')  # Redirect to cart page after adding

# View to display the cart
class CartView(View):
    def get(self, request):
        cart_data = Cart.objects.all()  # Adjust for user-specific data if needed
        return render(request, 'cart.html', {'cart_data': cart_data})


# Remove item from the cart
class RemoveFromCartView(View):
    def post(self, request, rep_id):
        Cart.objects.filter(rep_id=rep_id).delete()  # Remove specific report from Cart model
        return redirect('cart')


# Buy Now (Redirect to checkout or confirmation page)
class BuyNowView(View):
    def post(self, request):
        cart_data = Cart.objects.all()  # Adjust for user-specific data if needed
        if cart_data:
            # Handle the checkout logic, e.g., redirect to payment page
            return redirect('checkout')  # You can create a checkout page if needed
        return redirect('home')  # If cart is empty, redirect to the homepage
