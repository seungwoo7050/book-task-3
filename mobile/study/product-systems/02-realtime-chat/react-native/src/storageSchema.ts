import { appSchema, tableSchema } from '@nozbe/watermelondb';

export const chatSchema = appSchema({
  version: 1,
  tables: [
    tableSchema({
      name: 'messages',
      columns: [
        { name: 'server_id', type: 'string', isOptional: true },
        { name: 'client_id', type: 'string' },
        { name: 'conversation_id', type: 'string' },
        { name: 'text', type: 'string' },
        { name: 'status', type: 'string' },
      ],
    }),
  ],
});

export const chatSchemaSummary = {
  version: 1,
  tableNames: ['messages'] as const,
};
