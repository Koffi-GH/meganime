var shippingFlag = '{{order.shipping_flag}}'

if (shippingFlag == 'False') {
    document.getElementById('shipping-destination').innerHTML = ''
}