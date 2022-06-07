function tConvert(e){var t=new Date(e);time_s=t.getHours()+":"+t.getMinutes();var n=time_s.split(":"),e=n[0],t=n[1],n=12<=e?"PM":"AM";return(e=(e%=12)||12)+":"+(t=t<10?"0"+t:t)+" "+n}var str_dt=function(e){var t=new Date(e),n=""+["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][t.getMonth()],e=""+t.getDate(),t=t.getFullYear();return n.length<2&&(n="0"+n),[(e=e.length<2?"0"+e:e)+" "+n,t].join(", ")},invoices_list=localStorage.getItem("invoices-list"),options=localStorage.getItem("option"),invoice_no=localStorage.getItem("invoice_no"),invoices=JSON.parse(invoices_list);let viewobj=invoices.find(e=>e.invoice_no===invoice_no);if(""!=viewobj&&"view-invoice"==options){let e;switch(viewobj.status){case"Paid":e="success";break;case"Refund":e="primary";break;case"Unpaid":e="warning";break;case"Cancel":e="danger"}document.getElementById("legal-register-no").innerHTML=viewobj.company_details.legal_registration_no,document.getElementById("email").innerHTML=viewobj.company_details.email,document.getElementById("website").href=viewobj.company_details.website,document.getElementById("website").innerHTML=viewobj.company_details.website,document.getElementById("contact-no").innerHTML=viewobj.company_details.contact_no,document.getElementById("address-details").innerHTML=viewobj.company_details.address,document.getElementById("zip-code").innerHTML=viewobj.company_details.zip_code,document.getElementById("invoice-no").innerHTML=viewobj.invoice_no,document.getElementById("invoice-date").innerHTML=str_dt(viewobj.date),document.getElementById("invoice-time").innerHTML=tConvert(viewobj.date),document.getElementById("payment-status").innerHTML=viewobj.status,document.getElementById("payment-status").classList.replace("badge-soft-success","badge-soft-"+e),document.getElementById("total-amount").innerHTML=viewobj.invoice_amount,document.getElementById("billing-name").innerHTML=viewobj.billing_address.full_name,document.getElementById("billing-address-line-1").innerHTML=viewobj.billing_address.address,document.getElementById("billing-phone-no").innerHTML=viewobj.billing_address.phone,document.getElementById("billing-tax-no").innerHTML=viewobj.billing_address.tax,document.getElementById("shipping-name").innerHTML=viewobj.shipping_address.full_name,document.getElementById("shipping-address-line-1").innerHTML=viewobj.shipping_address.address,document.getElementById("shipping-phone-no").innerHTML=viewobj.shipping_address.phone,document.getElementById("products-list").innerHTML="";var paroducts_list=viewobj.prducts,counter=1;paroducts_list.forEach(function(e){product_data=`
            <tr>
                <th scope="row">`+counter+`</th>
                <td class="text-start">
                    <span class="fw-medium">`+e.product_name+`</span>
                    <p class="text-muted mb-0">`+e.product_details+`</p>
                </td>
                <td>`+e.rates+`</td>
                <td>`+e.quantity+`</td>
                <td class="text-end">$`+e.amount+`</td>
            </tr>`,document.getElementById("products-list").innerHTML+=product_data,counter++});var order_summary=`
        <tr class="border-top border-top-dashed mt-2">
            <td colspan="3"></td>
            <td colspan="2" class="fw-medium p-0">
                <table class="table table-borderless text-start table-nowrap align-middle mb-0">
                    <tbody>
                        <tr>
                            <td>Sub Total</td>
                            <td class="text-end">$`+viewobj.order_summary.sub_total+`</td>
                        </tr>
                        <tr>
                            <td>Estimated Tax (12.5%)</td>
                            <td class="text-end">$`+viewobj.order_summary.estimated_tex+`</td>
                        </tr>
                        <tr>
                            <td>Discount <small class="text-muted">(VELZON15)</small></td>
                            <td class="text-end">- $`+viewobj.order_summary.discount+`</td>
                        </tr>
                        <tr>
                            <td>Shipping Charge</td>
                            <td class="text-end">$`+viewobj.order_summary.shipping_charge+`</td>
                        </tr>
                        <tr class="border-top border-top-dashed">
                            <th scope="row">Total Amount</th>
                            <td class="text-end">$`+viewobj.order_summary.total_amount+`</td>
                        </tr>
                    </tbody>
                </table><!--end table-->
            </td>
        </tr>`;document.getElementById("products-list").innerHTML+=order_summary,document.getElementById("payment-method").innerHTML=viewobj.payment_details.payment_method,document.getElementById("card-holder-name").innerHTML=viewobj.payment_details.card_holder_name,document.getElementById("card-number").innerHTML=viewobj.payment_details.card_number,document.getElementById("card-total-amount").innerHTML=viewobj.payment_details.total_amount,document.getElementById("note").innerHTML=viewobj.notes}