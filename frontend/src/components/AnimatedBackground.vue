<template>
  <div class="fixed inset-0 z-0 overflow-hidden pointer-events-none">
    <span
      v-for="(item, i) in items"
      :key="i"
      :style="itemStyle(item)"
      class="absolute text-6xl animate-float"
    >
      {{ item.emoji }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import type { CSSProperties } from 'vue';

const EMOJI_COUNT = 18;
const emojis = [
  '💊', '🛍️', '🛒', '🧴', '🧃', '🧪', '🩹', '🍥', '🧘‍', '🩷', '🚩', '💉', '🧂', '🧫', '🧬', '🧻', '🧼', '🧯', '🧊', '🧃', '🧴'
];

function randomBetween(a: number, b: number) {
  return a + Math.random() * (b - a);
}

function createEmoji(i: number) {
  return {
    emoji: emojis[i % emojis.length],
    x: randomBetween(0, 90), // %
    y: randomBetween(0, 90), // %
    size: randomBetween(2.5, 5), // rem
    angle: randomBetween(0, 2 * Math.PI), // направление движения
    speed: randomBetween(0.2, 0.7), // % экрана в секунду
    rotate: randomBetween(0, 360),
  };
}

const items = ref(Array.from({ length: EMOJI_COUNT }, (_, i) => createEmoji(i)));
let animationFrame: number;

function moveEmojis(delta: number) {
  for (const item of items.value) {
    // Двигаем по направлению
    item.x += Math.cos(item.angle) * item.speed * delta;
    item.y += Math.sin(item.angle) * item.speed * delta;
    // Если вышли за границу — отражаем направление
    if (item.x < 0 || item.x > 95) {
      item.angle = Math.PI - item.angle + randomBetween(-0.2, 0.2);
      item.x = Math.max(0, Math.min(95, item.x));
    }
    if (item.y < 0 || item.y > 95) {
      item.angle = -item.angle + randomBetween(-0.2, 0.2);
      item.y = Math.max(0, Math.min(95, item.y));
    }
  }
}

let lastTime = performance.now();
function animate() {
  const now = performance.now();
  const delta = (now - lastTime) / 1000; // секунды
  moveEmojis(delta);
  lastTime = now;
  animationFrame = requestAnimationFrame(animate);
}

onMounted(() => {
  lastTime = performance.now();
  animationFrame = requestAnimationFrame(animate);
});
onUnmounted(() => {
  cancelAnimationFrame(animationFrame);
});

function itemStyle(item: any): CSSProperties {
  return {
    top: `${item.y}%`,
    left: `${item.x}%`,
    fontSize: `${item.size * 1.2}rem`,
    textShadow: '0 2px 8px rgba(0,0,0,0.18)',
    transform: `rotate(${item.rotate}deg)`,
    opacity: 0.35,
    position: 'absolute',
    transition: 'none',
    pointerEvents: 'none' as CSSProperties['pointerEvents'],
  };
}
</script>

<style scoped>
/* Убираем анимацию float, всё движение через JS */
</style> 