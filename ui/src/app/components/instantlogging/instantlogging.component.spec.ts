import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InstantloggingComponent } from './instantlogging.component';

describe('InstantloggingComponent', () => {
  let component: InstantloggingComponent;
  let fixture: ComponentFixture<InstantloggingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InstantloggingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InstantloggingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
