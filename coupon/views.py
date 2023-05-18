from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.forms import Form
from .forms import CouponApplyForm
from .models import Coupon


@require_POST
def coupon_apply(request: HttpRequest) -> HttpResponse:
    """A function to apply coupon disscount to orders.

        Only apply discount if all Coupon model field discriptors checks out
    """
    now = timezone.now()
    form: Form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            
            # Save coupon to user session
            request.session['coupon_id'] = coupon.id

        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart-detail')
