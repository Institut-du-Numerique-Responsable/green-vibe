// Fixture: non-conforming Angular
import { Component } from '@angular/core';
@Component({ selector: 'app-orders', templateUrl: './orders.html' })
export class OrdersComponent {
  ngOnInit() { this.svc.orders$.subscribe(o => this.orders = o); }
}
