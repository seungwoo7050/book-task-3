import { randomUUID } from "node:crypto";

import * as bcrypt from "bcryptjs";
import { type DataSource } from "typeorm";

import { Role, User } from "../auth/entities/user.entity";
import { Book } from "../books/entities/book.entity";

export async function seedDatabase(dataSource: DataSource): Promise<void> {
  const userRepository = dataSource.getRepository(User);
  const bookRepository = dataSource.getRepository(Book);

  const adminUsername = "admin";
  const demoUser = await userRepository.findOneBy({ username: adminUsername });

  if (!demoUser) {
    const password = await bcrypt.hash("admin123", 10);
    await userRepository.save(
      userRepository.create({
        id: randomUUID(),
        username: adminUsername,
        password,
        role: Role.ADMIN,
      }),
    );
  }

  if ((await bookRepository.count()) === 0) {
    await bookRepository.save([
      bookRepository.create({
        id: randomUUID(),
        title: "Designing Data-Intensive Applications",
        author: "Martin Kleppmann",
        publishedYear: 2017,
        genre: "Architecture",
        price: 49.99,
      }),
      bookRepository.create({
        id: randomUUID(),
        title: "Clean Architecture",
        author: "Robert C. Martin",
        publishedYear: 2017,
        genre: "Engineering",
        price: 32.0,
      }),
    ]);
  }
}
