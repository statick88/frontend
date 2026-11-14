import { ComponentFixture, TestBed } from '@angular/core/testing';

import { App } from './app';

describe('App', () => {
  let fixture: ComponentFixture<App>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
    }).compileComponents();

    fixture = TestBed.createComponent(App);
    fixture.detectChanges();
  });

  it('renders the neutral startup heading', () => {
    expect(fixture.nativeElement.querySelector('h1')?.textContent).toContain(
      'Proyecto Integrador',
    );
  });
});
