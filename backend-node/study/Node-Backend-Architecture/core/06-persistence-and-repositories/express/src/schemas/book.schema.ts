import { z } from "zod";

export const CreateBookSchema = z.object({
  title: z.string().min(1, "Title is required").max(200),
  author: z.string().min(1, "Author is required").max(100),
  publishedYear: z.number().int().min(1000).max(2100),
  genre: z.string().min(1, "Genre is required").max(50),
  price: z.number().positive("Price must be positive"),
});

export const UpdateBookSchema = z.object({
  title: z.string().min(1).max(200).optional(),
  author: z.string().min(1).max(100).optional(),
  publishedYear: z.number().int().min(1000).max(2100).optional(),
  genre: z.string().min(1).max(50).optional(),
  price: z.number().positive().optional(),
});

export type CreateBookDto = z.infer<typeof CreateBookSchema>;
export type UpdateBookDto = z.infer<typeof UpdateBookSchema>;
