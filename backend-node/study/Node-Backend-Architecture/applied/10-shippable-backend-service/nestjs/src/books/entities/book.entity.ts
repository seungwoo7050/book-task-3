import {
  Entity,
  PrimaryColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from "typeorm";
import { ApiProperty } from "@nestjs/swagger";

@Entity("books")
export class Book {
  @ApiProperty()
  @PrimaryColumn("uuid")
  id!: string;

  @ApiProperty()
  @Column({ type: "varchar", length: 200 })
  title!: string;

  @ApiProperty()
  @Column({ type: "varchar", length: 100 })
  author!: string;

  @ApiProperty()
  @Column("integer")
  publishedYear!: number;

  @ApiProperty()
  @Column({ type: "varchar", length: 50 })
  genre!: string;

  @ApiProperty()
  @Column("double precision")
  price!: number;

  @ApiProperty()
  @CreateDateColumn({ type: "timestamptz" })
  createdAt!: Date;

  @ApiProperty()
  @UpdateDateColumn({ type: "timestamptz" })
  updatedAt!: Date;
}
