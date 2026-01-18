<li attr="value"
    *ngFor="let hero of heroes as test"
    [class.selected]="hero === selectedHero"
    (click)="onSelect(hero)">
  {{hero.name}}
</li>

@for (hero of heroes; track heroes.name) {
  {{hero.name}}
} @empty {
  <p>No heroes!</p>
}

<div *ngIf="heroSig() as hero">{{hero.name}}</div>

{heroes.length, plural, =0 {no heroes} =1 {one hero} other {{{heroes.length}} heroes}} found

<input [(ngModel)]="selectedHero.name" #model="ngModel"/>
