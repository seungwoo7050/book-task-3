import { Request, Response } from "express";
import { AuthService } from "../services/auth.service";

export class AuthController {
  constructor(private readonly authService: AuthService) {
    this.register = this.register.bind(this);
    this.login = this.login.bind(this);
  }

  async register(req: Request, res: Response): Promise<void> {
    const { username, password, role } = req.body;
    const user = await this.authService.register({ username, password, role });

    if (!user) {
      res.status(409).json({ error: "Username already exists" });
      return;
    }

    res.status(201).json(user);
  }

  async login(req: Request, res: Response): Promise<void> {
    const { username, password } = req.body;
    const result = await this.authService.login(username, password);

    if (!result) {
      res.status(401).json({ error: "Invalid credentials" });
      return;
    }

    res.json(result);
  }
}
