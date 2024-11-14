from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Title, Datatable, Category, Report_price, Cart


class HomeView(View):
    def get(self, request):
        titles = Title.objects.all()  # Fetch all reports
        return render(request, 'index.html', {'titles': titles})


class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()  # Change to 'categories'
        return render(request, 'category.html', {'categories': categories})


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
            # Return to the info page with an error message if no license is selected
            return render(request, 'info.html', {
                'title': title,
                'datatable': get_object_or_404(Datatable, rep_id=rep_id),
                'category_name': get_object_or_404(Category, rep_category_id=title.rep_category_id).category_name,
                'buying_options': Report_price.objects.all(),
                'error_message': "You must select a license option before adding to cart."
            })

        # Get the selected price based on the license option
        price = get_object_or_404(Report_price, label=selected_option)

        # Check if the report is already in the cart
        cart_item, created = Cart.objects.get_or_create(
            rep_id=title,
            defaults={
                'rep_title': title.rep_title,
                'price': price.price,
                'label': price.label,
            }
        )

        if not created:
            # Update price if item already exists in the cart
            cart_item.price = price.price
            cart_item.label = price.label
            cart_item.save()

        return redirect('cart')


# View to display the cart
class CartView(View):
    def get(self, request):
        cart_data = Cart.objects.all()  # Adjust for user-specific data if needed
        report_prices = Report_price.objects.all()  # Fetch all price options

        return render(request, 'cart.html', {
            'cart_data': cart_data,
            'report_prices': report_prices
        })


class UpdatePriceView(View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        price_option_id = request.POST.get('price_option')

        # Fetch the cart item and the selected price option
        cart_item = get_object_or_404(Cart, id=cart_id)
        selected_price_option = get_object_or_404(Report_price, price_id=price_option_id)

        # Update the cart item with the new price and label
        cart_item.price = selected_price_option.price
        cart_item.label = selected_price_option.label
        cart_item.save()

        return redirect('cart')


class Remove(View):
    def post(self, request):
        rep_id = request.POST.get('id')  # Get ID from POST data
        if rep_id:
            # Remove item from Cart model based on rep_id
            Cart.objects.filter(id=rep_id).delete()
        return redirect('cart')  # Redirect to the cart page


# Buy Now (Redirect to checkout or confirmation page)
class BuyNowView(View):
    def post(self, request):
        cart_data = Cart.objects.all()  # Adjust for user-specific data if needed
        if cart_data:
            # Handle the checkout logic, e.g., redirect to payment page
            return redirect('checkout')  # You can create a checkout page if needed
        return redirect('home')  # If cart is empty, redirect to the homepage
