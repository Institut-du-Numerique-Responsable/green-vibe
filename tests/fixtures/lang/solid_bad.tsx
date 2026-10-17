// Fixture: non-conforming Solid
import { createEffect, createSignal } from 'solid-js';
export function List(props) {
  createEffect(() => console.log(props.store.items.length));
  return <ul>{props.items.map((i) => <li>{i}</li>)}</ul>;
}
