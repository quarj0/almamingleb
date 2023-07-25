

# def initiate_coin_purchase(request):
#     # Get the coin purchase amount from the POST request data
#     amount = request.POST.get('amount')

#     # Define the MoMoDeveloper API endpoint and payload
#     url = 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay'
#     payload = {
#         'amount': amount,
#         'currency': 'GHS',
#         'externalId': '496135',
#         'payer': {
#             'partyIdType': 'MSISDN',
#             'partyId': '233559537405' # Replace with the user's mobile money number
#         },
#         'payerMessage': 'Payment for coins',
#         'payeeNote': 'Note for payee'
#     }

#     # Make the API request with authentication headers
#     response = requests.post(url, json=payload, headers={
#         'Authorization': f'Bearer {settings.MOMO_API_KEY}',
#         'Ocp-Apim-Subscription-Key': settings.MOMO_API_SECRET,
#         'Content-Type': 'application/json'
#     })

#     # Handle the response from the MoMoDeveloper API
#     if response.status_code == 202:
#         # The payment request was successful, save the coin purchase to the database
#         coin_purchase = CoinPurchase.objects.create(
#             user=request.user,
#             amount=amount,
#             price=amount / 10, # Replace with the actual price calculation
#             payment_method='MTN Mobile Money',
#         )
#         return JsonResponse({'success': True})
#     else:
#         # The payment request failed, return an error response
#         return JsonResponse({'success': False, 'error': response.json()})

# class CoinList(generics.ListAPIView):
#     queryset = Coin.objects.all()
#     serializer_class = CoinSerializer


# class CoinPurchaseList(generics.ListCreateAPIView):
#     serializer_class = CoinPurchaseSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return CoinPurchase.objects.filter(user=user)


# class CoinPurchaseDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = CoinPurchaseSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return CoinPurchase.objects.filter(user=user)
