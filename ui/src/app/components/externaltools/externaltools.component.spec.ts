import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExternaltoolsComponent } from './externaltools.component';

describe('ExternaltoolsComponent', () => {
  let component: ExternaltoolsComponent;
  let fixture: ComponentFixture<ExternaltoolsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExternaltoolsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExternaltoolsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
