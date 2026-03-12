import {
  Entity,
  PrimaryColumn,
  Column,
  CreateDateColumn,
} from "typeorm";
import { ApiProperty } from "@nestjs/swagger";

export enum Role {
  USER = "USER",
  ADMIN = "ADMIN",
}

@Entity("users")
export class User {
  @ApiProperty()
  @PrimaryColumn("uuid")
  id!: string;

  @ApiProperty()
  @Column({ type: "varchar", length: 30, unique: true })
  username!: string;

  @Column({ type: "varchar", length: 100 })
  password!: string;

  @ApiProperty({ enum: Role, enumName: "Role" })
  @Column({ type: "varchar", length: 10, default: Role.USER })
  role!: Role;

  @ApiProperty()
  @CreateDateColumn({ type: "timestamptz" })
  createdAt!: Date;
}
