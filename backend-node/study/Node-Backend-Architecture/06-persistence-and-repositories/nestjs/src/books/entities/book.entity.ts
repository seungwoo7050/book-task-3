import {
  Entity,
  PrimaryColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from "typeorm";

@Entity("books")
export class Book {
  @PrimaryColumn("text")
  id!: string;

  @Column({ type: "text" })
  title!: string;

  @Column({ type: "text" })
  author!: string;

  @Column("integer")
  publishedYear!: number;

  @Column({ type: "text" })
  genre!: string;

  @Column("real")
  price!: number;

  @CreateDateColumn({ type: "datetime" })
  createdAt!: Date;

  @UpdateDateColumn({ type: "datetime" })
  updatedAt!: Date;
}
