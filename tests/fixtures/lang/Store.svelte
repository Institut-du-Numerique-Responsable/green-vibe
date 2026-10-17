<script>
  // Fixture: non-conforming Svelte
  import { items } from './stores.js';
  items.subscribe(v => list = v);
  $: {
    total = list.length;
  }
</script>
