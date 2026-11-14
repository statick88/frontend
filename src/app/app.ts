import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
    <main>
      <h1>Proyecto Integrador</h1>
    </main>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App {}
