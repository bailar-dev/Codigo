(() => {
  const money = n => new Intl.NumberFormat('az-AZ', { minimumFractionDigits:2, maximumFractionDigits:2 }).format(n);
  document.querySelectorAll('[data-billing]').forEach(b => b.addEventListener('click', () => {
    const annual = b.dataset.billing === 'annual';
    document.querySelectorAll('[data-billing]').forEach(x => x.setAttribute('aria-pressed',String(x===b)));
    document.getElementById('plusPrice').textContent = annual ? '8,25' : '9,90';
    document.getElementById('plusBilling').textContent = annual ? 'İldə bir dəfə 99 AZN ödəniş · aylıq ekvivalent' : 'Aylıq ödəniş: 9,90 AZN';
    document.getElementById('plusSaving').textContent = annual ? '12 aylıq ödənişlə müqayisədə 19,80 AZN qənaət.' : 'İllik seçim: 99 AZN / il. 19,80 AZN qənaət.';
  }));
  const seats=document.getElementById('seatCount');
  if(seats) seats.addEventListener('input',()=>{
    const n=Number(seats.value), valid=seats.value.trim()!=='' && Number.isInteger(n) && n>=25 && n<=200;
    seats.setAttribute('aria-invalid',String(!valid));
    document.getElementById('seatError').textContent=valid?'':n>200?'200-dən çox yer üçün müəssisə təklifi seçin.':'25–200 arasında tam ədəd daxil edin.';
    const total=149+(n-25)*4.9;
    document.getElementById('classTotal').textContent=valid?money(total)+' AZN':'—';
    document.getElementById('perSeat').textContent=valid?money(total/n)+' AZN / ay':'—';
  });
  const plan=document.getElementById('fPlan');
  if(plan){const requested=new URLSearchParams(location.search).get('plan');if(['plus','sinif','muessise','pilot'].includes(requested))plan.value=requested;}
})();
