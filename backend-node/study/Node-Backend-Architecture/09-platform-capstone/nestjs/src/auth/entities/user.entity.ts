import {
  Entity,
  PrimaryColumn,
  Column,
  CreateDateColumn,
} from "typeorm";

export enum Role {
  USER = "USER",
  ADMIN = "ADMIN",
}

@Entity("users")
export class User {
  @PrimaryColumn("text")
  id!: string;

  @Column({ type: "text", unique: true })
  username!: string;

  @Column({ type: "text" })
  password!: string;

  @Column({ type: "text", default: Role.USER })
  role!: Role;

  @CreateDateColumn({ type: "datetime" })
  createdAt!: Date;
}
