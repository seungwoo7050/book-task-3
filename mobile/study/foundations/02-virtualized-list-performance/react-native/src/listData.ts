export type ItemKind = 'text' | 'image' | 'card';

export interface StudyListItem {
  id: string;
  type: ItemKind;
  title: string;
  subtitle: string;
  imageUrl?: string;
  tags: string[];
  timestamp: number;
}

const ITEM_TYPES: ItemKind[] = ['text', 'image', 'card'];

function seededFloat(seed: number): number {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

export function itemHeightForType(type: ItemKind): number {
  switch (type) {
    case 'text':
      return 92;
    case 'image':
      return 232;
    case 'card':
      return 156;
  }
}

export function createDeterministicItems(seed: number, count: number): StudyListItem[] {
  return Array.from({ length: count }, (_, index) => {
    const type = ITEM_TYPES[index % ITEM_TYPES.length];
    const sample = Math.floor(seededFloat(seed + index) * 1000);

    return {
      id: `item-${seed}-${index}`,
      type,
      title: `${type.toUpperCase()} item ${index + 1}`,
      subtitle: `seed:${seed} sample:${sample}`,
      imageUrl:
        type === 'image'
          ? `https://picsum.photos/seed/${seed + index}/200/120`
          : undefined,
      tags: [`group-${index % 7}`, `bucket-${sample % 5}`],
      timestamp: 1700000000000 + index * 30000,
    };
  });
}
