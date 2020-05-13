import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AhomeTermComponent } from './ahome-term.component';

describe('AhomeTermComponent', () => {
  let component: AhomeTermComponent;
  let fixture: ComponentFixture<AhomeTermComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AhomeTermComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AhomeTermComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
